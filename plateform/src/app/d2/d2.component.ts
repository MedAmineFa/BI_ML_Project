import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-d2',
  templateUrl: './d2.component.html',
  styleUrls: ['./d2.component.css']
})
export class D2Component {
  constructor(private router: Router) {}

  goBack() {
    // Vous pouvez rediriger vers une autre page ici si nécessaire
    this.router.navigate(['/gestion-du-budget']); // Redirige vers la page d'accueil
  }
}
