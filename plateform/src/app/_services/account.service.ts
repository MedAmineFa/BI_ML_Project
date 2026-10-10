import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { environment } from '@environments/environment';
import { User, Role } from '@app/_models';

@Injectable({ providedIn: 'root' })
export class AccountService {
    private userSubject: BehaviorSubject<User | null>;
    public user: Observable<User | null>;

    constructor(
        private router: Router,
        private http: HttpClient
    ) {
        this.userSubject = new BehaviorSubject<User | null>(JSON.parse(localStorage.getItem('user') || 'null'));
        this.user = this.userSubject.asObservable();
    }

    public get userValue() {
        return this.userSubject.value;
    }

    login(username: string, password: string) {
        return this.http.post<User>(`${environment.apiUrl}/users/authenticate`, { username, password })
            .pipe(map(user => {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(user));
                this.userSubject.next(user);
                return user;
            }));
    }

    logout() {
        // remove user from local storage and set current user to null
        localStorage.removeItem('user');
        this.userSubject.next(null);
        this.router.navigate(['/account/login']);
    }
    
    refreshToken() {
        return this.http.post<any>(`${environment.apiUrl}/users/refresh-token`, {}, { withCredentials: true })
            .pipe(map((user) => {
                this.userSubject.next(user);
                this.startRefreshTokenTimer();
                return user;
            }));
    }
    register(user: User) {
        // Get the total number of registered users from local storage
        const totalUsers = JSON.parse(localStorage.getItem('totalUsers') || '0');
    
        // Increment the total number of registered users
        localStorage.setItem('totalUsers', JSON.stringify(totalUsers + 1));
    
        // Register the user
        return this.http.post(`${environment.apiUrl}/users/register`, user);
    }
    forgotPassword(email: string) {
        return this.http.post(`${environment.apiUrl}/users/forgot-password`, { email });
    }
    
    validateResetToken(token: string) {
        return this.http.post(`${environment.apiUrl}/users/validate-reset-token`, { token });
    }

    resetPassword(token: string, password: string, confirmPassword: string) {
        return this.http.post(`${environment.apiUrl}/users/reset-password`, { token, password, confirmPassword });
    }
    getAll() {
        return this.http.get<User[]>(`${environment.apiUrl}/users`);
    }

    getById(id: string) {
        return this.http.get<User>(`${environment.apiUrl}/users/${id}`);
    }
    private refreshTokenTimeout?: any;

    private startRefreshTokenTimer() {
        // parse json object from base64 encoded jwt token
        const jwtBase64 = this.userValue!.token!.split('.')[1];
        const jwtToken = JSON.parse(atob(jwtBase64));

        // set a timeout to refresh the token a minute before it expires
        const expires = new Date(jwtToken.exp * 1000);
        const timeout = expires.getTime() - Date.now() - (60 * 1000);
        this.refreshTokenTimeout = setTimeout(() => this.refreshToken().subscribe(), timeout);
    }

    update(id: string, params: any) {
        return this.http.put(`${environment.apiUrl}/users/${id}`, params)
            .pipe(map(x => {
                // update stored user if the logged in user updated their own record
                if (id == this.userValue?.id) {
                    // update local storage
                    const user = { ...this.userValue, ...params };
                    localStorage.setItem('user', JSON.stringify(user));

                    // publish updated user to subscribers
                    this.userSubject.next(user);
                }
                return x;
            }));
    }

    delete(id: string) {
        return this.http.delete(`${environment.apiUrl}/users/${id}`)
            .pipe(map(x => {
                // auto logout if the logged in user deleted their own record
                if (id == this.userValue?.id) {
                    this.logout();
                }
                return x;
            }));
    }
    
    updateActivation(id: string, activationStatus: number) {
        const params = { activation: activationStatus };
        return this.http.put(`${environment.apiUrl}/users/${id}`, params)
            .pipe(map(response => {
                // Update stored user if the logged-in user updated their own record
                if (id === this.userValue?.id) {
                    // Update local storage
                    const updatedUser = { ...this.userValue, activation: activationStatus };
                    localStorage.setItem('user', JSON.stringify(updatedUser));
                    
                    // Publish updated user to subscribers
                    this.userSubject.next(updatedUser);
                }
                return response;
            }));
    }
    
    updateRole(id: string, newRole: Role) {
        const params = { role: newRole };
    
        return this.http.put(`${environment.apiUrl}/users/${id}`, params)
            .pipe(map(response => {
                // Update stored user if the logged-in user updated their own record
                if (id === this.userValue?.id) {
                    // Update local storage
                    const updatedUser = { ...this.userValue, role: newRole };
                    localStorage.setItem('user', JSON.stringify(updatedUser));
                    
                    // Publish updated user to subscribers
                    this.userSubject.next(updatedUser);
                }
                return response;
            }));
    }
}
