import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { WebserviceService } from '../../services/webservice.service';

@Component({
  selector: 'app-book-tee-time',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './book-tee-time.component.html',
  styleUrls: ['./book-tee-time.component.css']
})
export class BookTeeTimeComponent implements OnInit {

  courses: any[] = [];
  teeTimes: any[] = [];

  course_id: number | null = null;
  date = '';

  constructor(
    private ws: WebserviceService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.ws.getCourses().subscribe({
      next: data => this.courses = data
    });
  }

  loadTeeTimes(): void {
    if (!this.course_id || !this.date) return;

    this.ws.getAvailableTeeTimes(this.course_id, this.date).subscribe({
      next: data => this.teeTimes = data,
      error: err => console.error(err)
    });
  }

  book(teeTimeId: number): void {
    this.ws.bookTeeTime(teeTimeId).subscribe({
      next: () => {
        alert('Tee time booked successfully');
        this.teeTimes = this.teeTimes.filter(t => t.id !== teeTimeId);
      },
      error: err => {
        if (err.status === 401) {
          this.router.navigate(['/login']);
        } else {
          alert('Failed to book tee time');
        }
      }
    });
  }

}
