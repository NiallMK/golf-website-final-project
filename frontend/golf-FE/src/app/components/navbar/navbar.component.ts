import { Component, OnInit } from '@angular/core';
import { WebserviceService } from '../../services/webservice.service';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  templateUrl: './navbar.component.html',
  imports: [CommonModule, RouterModule],
})
export class NavbarComponent implements OnInit {

  user: any;

  constructor(private ws: WebserviceService) {}

  ngOnInit(): void {
    this.ws.getUser(1).subscribe({
      next: (data) => {
        console.log('USER DATA:', data);
        this.user = data;
      },
      error: (err) => {
        console.error('USER ERROR:', err);
      }
    });
  }

}


