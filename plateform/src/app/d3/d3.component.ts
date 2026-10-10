import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-d3',
  templateUrl: './d3.component.html',
  styleUrls: ['./d3.component.css']
})
export class D3Component implements OnInit {

  constructor(private router: Router) {}

  ngOnInit(): void {
  }

  goBack() {
    // Vous pouvez rediriger vers une autre page ici si nécessaire
    this.router.navigate(['/gestion-des-achats']);
  }
}
