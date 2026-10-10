import { Component } from '@angular/core';
import { AccountService } from './_services';
import { User } from './_models';

@Component({ 
    selector: 'app-root', 
    templateUrl: 'app.component.html',
    styleUrls: ['app.component.css'],
})
export class AppComponent {
    user?: User | null;
    hideLinks = true; // Initially set to true to hide links when no user is logged in
    isAdmin = false; // Initially assume the user is not an admin

    constructor(private accountService: AccountService) {
        this.accountService.user.subscribe(x => {
            this.user = x;
            // Update hideLinks based on user login status
            this.hideLinks = !x; // If user exists, hideLinks is false, otherwise true
            // Check if the user is an admin
            this.isAdmin = x ? x.role === 'Admin' : false;
        });
    }

    logout() {
        this.accountService.logout();
    }
}
