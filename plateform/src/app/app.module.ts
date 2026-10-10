import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

// Import your interceptors and other components if necessary
import { AppRoutingModule } from './app-routing.module';
import { JwtInterceptor, ErrorInterceptor, fakeBackendProvider } from './_helpers';
import { AppComponent } from './app.component';
import { AlertComponent } from './_components';
import { HomeComponent } from './home';
import { GestionDesAchatsComponent } from './gestion-des-achats/gestion-des-achats.component';
import { GestionDuBudgetComponent } from './gestion-du-budget/gestion-du-budget.component';
import { D1Component } from './d1/d1.component';
import { D2Component } from './d2/d2.component';
import { D3Component } from './d3/d3.component';
import { D4Component } from './d4/d4.component';
import { PredictionComponent } from './prediction/prediction.component';

@NgModule({
    imports: [
        BrowserModule,
        ReactiveFormsModule,
        HttpClientModule,
        AppRoutingModule
    ],
    declarations: [
        AppComponent,
        AlertComponent,
        HomeComponent,
        GestionDesAchatsComponent,
        GestionDuBudgetComponent,
        D1Component,
        D2Component,
        D3Component,
        D4Component,
        PredictionComponent
    ],
    providers: [
        { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
        { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
        fakeBackendProvider
    ],
    
    bootstrap: [AppComponent]
})
export class AppModule { }
