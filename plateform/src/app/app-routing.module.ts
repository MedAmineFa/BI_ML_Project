import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from './home';
import { AuthGuard } from './_helpers';

const accountModule = () => import('./account/account.module').then(x => x.AccountModule);
const usersModule = () => import('./users/users.module').then(x => x.UsersModule);
import { GestionDuBudgetComponent } from './gestion-du-budget/gestion-du-budget.component';
import { GestionDesAchatsComponent } from './gestion-des-achats/gestion-des-achats.component';
import { D1Component } from './d1/d1.component'; 
import { D2Component } from './d2/d2.component';
import { D3Component } from './d3/d3.component'; 
import { D4Component } from './d4/d4.component';
import { PredictionComponent } from './prediction/prediction.component';

const routes: Routes = [
    { path: '', component: HomeComponent, canActivate: [AuthGuard] },
    { path: 'users', loadChildren: usersModule, canActivate: [AuthGuard] },
    { path: 'account', loadChildren: accountModule },
    { path: 'gestion-des-achats', component: GestionDesAchatsComponent, canActivate: [AuthGuard] },
    { path: 'gestion-du-budget', component: GestionDuBudgetComponent, canActivate: [AuthGuard] },
    { path: 'd1', component: D1Component },
    { path: 'd2', component: D2Component },
    { path: 'd3', component: D3Component },
    { path: 'd4', component: D4Component },
    { path: 'prediction', component: PredictionComponent },

    // otherwise redirect to home
    { path: '**', redirectTo: '' }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
