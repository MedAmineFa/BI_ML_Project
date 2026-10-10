import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-d4',
  templateUrl: './d4.component.html',
  styleUrls: ['./d4.component.css']
})
export class D4Component implements OnInit {

  constructor(private router: Router) {}

  ngOnInit(): void {
  }
  goBack() {
    // Vous pouvez rediriger vers une autre page ici si nécessaire
    this.router.navigate(['/gestion-des-achats']);
  }
}
