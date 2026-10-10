import { Component, OnInit } from '@angular/core';
import { first } from 'rxjs/operators';
import { User, Role } from '@app/_models';

import { AccountService } from '@app/_services';
@Component({ templateUrl: 'list.component.html' })
export class ListComponent implements OnInit {
    users?: any[];
    loggedInUserId!: number; // Initialize loggedInUserId with an exclamation mark

    constructor(private accountService: AccountService) {
    }

    ngOnInit() {
        this.loadUsers();
        // Assuming you have a way to retrieve the ID of the logged-in user, 
        // assign it to the loggedInUserId property
        // Example: this.loggedInUserId = /* Code to retrieve the ID of the logged-in user */;
    }

    loadUsers() {
        this.accountService.getAll()
            .pipe(first())
            .subscribe(users => this.users = users);
    }

    deleteUser(id: string) {
        const user = this.users!.find(x => x.id === id);
        user.isDeleting = true;
        this.accountService.delete(id)
            .pipe(first())
            .subscribe(() => {
                this.users = this.users!.filter(x => x.id !== id);
                delete user.isDeleting;
            });
    }

    toggleActivation(user: any) {
        const newActivation = user.activation === 1 ? 0 : 1; // Toggle activation
    
        this.accountService.updateActivation(user.id, newActivation) // Update the user's activation status
            .subscribe(() => {
                user.activation = newActivation; // Update the user's activation property in the local array
            });
    }   

    toggleUserRole(user: any) {
        const newRole = user.role === Role.Admin ? Role.User : Role.Admin; // Toggle role
    
        this.accountService.updateRole(user.id, newRole) // Update the user's role
            .subscribe(() => {
                user.role = newRole; // Update the user's role property in the local array
            });
    }    
}
