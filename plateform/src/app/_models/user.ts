import { Role } from './role';

export class User {
    id?: string;
    email?: string;
    username?: string;
    password?: string;
    firstName?: string;
    lastName?: string;
    role?: Role;
    activation?: number;
    token?: string;
}