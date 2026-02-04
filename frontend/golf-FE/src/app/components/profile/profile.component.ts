import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WebserviceService } from '../../services/webservice.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  profile: any;
  user_id = 1; // TEMP

  constructor(private ws: WebserviceService) {}
  
  bookings: any[] = [];

  ngOnInit(): void {
    this.ws.getUserProfile(this.user_id).subscribe({
      next: data => this.profile = data,
      error: err => console.error(err)
    });

    this.ws.getUserBookings(this.user_id).subscribe({
      next: data => this.bookings = data,
      error: err => console.error(err)
    });

  }


}

