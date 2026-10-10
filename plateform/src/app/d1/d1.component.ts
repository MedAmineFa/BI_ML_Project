import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-d1',
  templateUrl: './d1.component.html',
  styleUrls: ['./d1.component.css']
})
export class D1Component {
  constructor(private router: Router) {}

  goBack() {
    // Vous pouvez rediriger vers une autre page ici si nécessaire
    this.router.navigate(['/gestion-du-budget']);
  }
}
