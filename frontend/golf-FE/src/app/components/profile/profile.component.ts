import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WebserviceService } from '../../services/webservice.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  profile: any;
  bookings: any[] = [];

  constructor(
    private ws: WebserviceService,
    private router: Router
  ) {}

  ngOnInit(): void {

    // -----------------------------
    // Load logged-in user's profile
    // -----------------------------
    this.ws.getUserProfile().subscribe({
      next: data => this.profile = data,
      error: err => {
        console.error(err);
        if (err.status === 401) {
          this.router.navigate(['/login']);
        }
      }
    });

    // -----------------------------
    // Load logged-in user's bookings
    // -----------------------------
    this.ws.getUserBookings().subscribe({
      next: data => this.bookings = data,
      error: err => {
        console.error(err);
        if (err.status === 401) {
          this.router.navigate(['/login']);
        }
      }
    });

  }

}
