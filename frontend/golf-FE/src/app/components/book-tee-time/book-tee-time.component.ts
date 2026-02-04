import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
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
  date: string = '';

  user_id = 1; // TEMP until auth

  constructor(private ws: WebserviceService) {}

  ngOnInit(): void {
    this.ws.getCourses().subscribe({
      next: data => this.courses = data
    });
  }

  loadTeeTimes() {
    if (!this.course_id || !this.date) return;

    this.ws.getAvailableTeeTimes(this.course_id, this.date).subscribe({
      next: data => this.teeTimes = data,
      error: err => console.error(err)
    });
  }

  book(teeTimeId: number) {
    this.ws.bookTeeTime(this.user_id, teeTimeId).subscribe({
      next: () => {
        alert('Tee time booked successfully');
        this.teeTimes = this.teeTimes.filter(t => t.id !== teeTimeId);
      },
      error: () => alert('Failed to book tee time')
    });
  }
}
