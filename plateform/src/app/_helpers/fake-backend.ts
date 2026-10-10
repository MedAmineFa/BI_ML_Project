import { Injectable } from '@angular/core';
import { HttpRequest, HttpResponse, HttpHandler, HttpEvent, HttpInterceptor, HTTP_INTERCEPTORS } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { delay, materialize, dematerialize } from 'rxjs/operators';
import { AlertService } from '@app/_services';
import { Role } from '@app/_models';

const usersKey = 'angular-14-registration-login-example-users';
let users: any[] = JSON.parse(localStorage.getItem(usersKey)!) || [];

@Injectable()
export class FakeBackendInterceptor implements HttpInterceptor {
    constructor(private AlertService: AlertService) { }
    
    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        const { url, method, headers, body } = request;
        const AlertService = this.AlertService;

        return handleRoute();

        function handleRoute() {
            switch (true) {
                case url.endsWith('/users/authenticate') && method === 'POST':
                    return authenticate();
                case url.endsWith('/users/refresh-token') && method === 'POST':
                    return refreshToken();
                case url.endsWith('/users/revoke-token') && method === 'POST':
                    return revokeToken();
                case url.endsWith('/users/register') && method === 'POST':
                    return register();
                case url.endsWith('/users/forgot-password') && method === 'POST':
                    return forgotPassword();   
                case url.endsWith('/users/validate-reset-token') && method === 'POST':
                    return validateResetToken();
                case url.endsWith('/users/reset-password') && method === 'POST':
                    return resetPassword();    
                case url.endsWith('/users') && method === 'GET':
                    return getUsers();
                case url.match(/\/users\/\d+$/) && method === 'GET':
                    return getUserById();
                case url.match(/\/users\/\d+$/) && method === 'PUT':
                    return updateUser();
                case url.match(/\/users\/\d+$/) && method === 'DELETE':
                    return deleteUser();
                default:
                    return next.handle(request);
            }    
        }

        function authenticate() {
            const { username, password } = body;
            const user = users.find(x => x.username === username && x.password === password);
            if (!user) return error('Nom d\'utilisateur ou mot de passe incorrect');
            if (user.activation === 0) return error('Compte utilisateur non activé. Veuillez attendre l\'administrateur.');
            return ok({
                ...basicDetails(user),
                token: 'fake-jwt-token'
            })
        }
        function refreshToken() {
            const refreshToken = getRefreshToken();
            
            if (!refreshToken) return unauthorized();

            const account = users.find(x => x.refreshTokens.includes(refreshToken));
            
            if (!account) return unauthorized();

            // replace old refresh token with a new one and save
            account.refreshTokens = account.refreshTokens.filter((x: any) => x !== refreshToken);
            account.refreshTokens.push(generateRefreshToken());
            localStorage.setItem(usersKey, JSON.stringify(users));

            return ok({
                ...basicDetails(account),
                jwtToken: generateJwtToken(account)
            });
        }
        function revokeToken() {
            if (!authenticate()) return unauthorized();
            
            const refreshToken = getRefreshToken();
            const account = users.find(x => x.refreshTokens.includes(refreshToken));
            
            // revoke token and save
            account.refreshTokens = account.refreshTokens.filter((x: any) => x !== refreshToken);
            localStorage.setItem(usersKey, JSON.stringify(users));

            return ok();
        }
        function register() {
            const user = body;
            if (users.find(x => x.username === user.username)) {
                return error('Username "' + user.username + '" is already taken')
            }
            if (users.find(x => x.email === user.email)) {
                return error('Email "' + user.email + '" is already taken')
            }
            user.id = users.length ? Math.max(...users.map(x => x.id)) + 1 : 1;
            if (user.id === 1) {
                user.role = Role.Admin;
                user.activation = 1;
            } else {
                user.role = Role.User;
                user.activation = 0;
            }
            users.push(user);
            user.verificationToken = new Date().getTime().toString();
            localStorage.setItem(usersKey, JSON.stringify(users));
            return ok();
        }

        function forgotPassword() {
            const { email } = body;
            const account = users.find(x => x.email === email);
            
            // always return ok() response to prevent email enumeration
            if (!account) return ok();
            
            // create reset token that expires after 24 hours
            account.resetToken = new Date().getTime().toString();
            account.resetTokenExpires = new Date(Date.now() + 24*60*60*1000).toISOString();
            localStorage.setItem(usersKey, JSON.stringify(users));

            // display password reset email in alert
            setTimeout(() => {
                const resetUrl = `${location.origin}/account/reset-password?token=${account.resetToken}`;
                AlertService.info(`
                    <h4>Email de réinitialisation du mot de passe</h4>
                    <p>Veuillez cliquer sur le lien ci-dessous pour réinitialiser votre mot de passe, le lien sera valide pendant 1 jour :</p>
                    <p><a href="${resetUrl}">${resetUrl}</a></p>
                    `, { autoClose: false });
            }, 1000);

            return ok();
        }
        
        function validateResetToken() {
            const { token } = body;
            const account = users.find(x =>
                !!x.resetToken && x.resetToken === token &&
                new Date() < new Date(x.resetTokenExpires)
            );
            
            if (!account) return error('Invalid token');
            
            return ok();
        }

        function resetPassword() {
            const { token, password } = body;
            const account = users.find(x =>
                !!x.resetToken && x.resetToken === token &&
                new Date() < new Date(x.resetTokenExpires)
            );
            
            if (!account) return error('Invalid token');
            
            // update password and remove reset token
            account.password = password;
            account.isVerified = true;
            delete account.resetToken;
            delete account.resetTokenExpires;
            localStorage.setItem(usersKey, JSON.stringify(users));

            return ok();
        }
        function getUsers() {
            if (!isLoggedIn()) return unauthorized();
            return ok(users.map(x => basicDetails(x)));
        }

        function getUserById() {
            if (!isLoggedIn()) return unauthorized();
            const user = users.find(x => x.id === idFromUrl());
            return ok(basicDetails(user));
        }

        function updateUser() {
            if (!isLoggedIn()) return unauthorized();
            let params = body;
            let user = users.find(x => x.id === idFromUrl());
            if (!params.password) {
                delete params.password;
            }
            Object.assign(user, params);
            localStorage.setItem(usersKey, JSON.stringify(users));
            return ok();
        }

        function deleteUser() {
            if (!isLoggedIn()) return unauthorized();
            users = users.filter(x => x.id !== idFromUrl());
            localStorage.setItem(usersKey, JSON.stringify(users));
            return ok();
        }

        function ok(body?: any) {
            return of(new HttpResponse({ status: 200, body })).pipe(delay(500));
        }

        function error(message: string) {
            return throwError(() => ({ error: { message } }))
                .pipe(materialize(), delay(500), dematerialize());
        }

        function unauthorized() {
            return throwError(() => ({ status: 401, error: { message: 'Unauthorized' } }))
                .pipe(materialize(), delay(500), dematerialize());
        }

        function basicDetails(user: any) {
            const { id, email, username, firstName, lastName, role, activation } = user;
            return { id, email, username, firstName, lastName, role, activation };
        }

        function isLoggedIn() {
            return headers.get('Authorization') === 'Bearer fake-jwt-token';
        }

        function idFromUrl() {
            const urlParts = url.split('/');
            return parseInt(urlParts[urlParts.length - 1]);
        }
        function generateJwtToken(account: any) {
            // create token that expires in 15 minutes
            const tokenPayload = { 
                exp: Math.round(new Date(Date.now() + 15*60*1000).getTime() / 1000),
                id: account.id
            }
            return `fake-jwt-token.${btoa(JSON.stringify(tokenPayload))}`;
        }

        function generateRefreshToken() {
            const token = new Date().getTime().toString();

            // add token cookie that expires in 7 days
            const expires = new Date(Date.now() + 7*24*60*60*1000).toUTCString();
            document.cookie = `fakeRefreshToken=${token}; expires=${expires}; path=/`;

            return token;
        }

        function getRefreshToken() {
            // get refresh token from cookie
            return (document.cookie.split(';').find(x => x.includes('fakeRefreshToken')) || '=').split('=')[1];
        }
    }
    
}

export const fakeBackendProvider = {
    provide: HTTP_INTERCEPTORS,
    useClass: FakeBackendInterceptor,
    multi: true
};
