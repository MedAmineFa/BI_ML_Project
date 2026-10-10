import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-gestion-des-achats',
  templateUrl: './gestion-des-achats.component.html',
  styleUrls: ['./gestion-des-achats.component.css']
})
export class GestionDesAchatsComponent implements OnInit {
  showMessage: boolean = false;
  message: string = '';
  selectedOption: string = '';

  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  showMessageAndHideButtons(option: string, message: string, event: Event) {
    this.showMessage = true;
    this.message = message;
    this.selectedOption = option;
    event.preventDefault(); // Prevent default navigation behavior
  }

  goBack() {
    this.showMessage = false;
    this.selectedOption = '';
  }
}
