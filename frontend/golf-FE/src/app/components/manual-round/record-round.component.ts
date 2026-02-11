import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { WebserviceService } from '../../services/webservice.service';

@Component({
  selector: 'app-record-round',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './record-round.component.html',
  styleUrls: ['./record-round.component.css']
})
export class RecordRoundComponent implements OnInit {

  // All courses from API
  courses: any[] = [];

  // Search + selection state
  courseSearch = '';
  filteredCourses: any[] = [];
  selectedCourse: any = null;

  // Form data
  course_id!: number;
  date_played = '';

  constructor(
    private ws: WebserviceService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.ws.getCourses().subscribe({
      next: data => this.courses = data,
      error: err => console.error(err)
    });
  }

  // -------------------------
  // Filter courses as user types
  // -------------------------
  filterCourses(): void {
    const query = this.courseSearch.toLowerCase().trim();

    if (!query) {
      this.filteredCourses = [];
      return;
    }

    this.filteredCourses = this.courses.filter(c =>
      c.name.toLowerCase().includes(query)
    );
  }

  // -------------------------
  // Select a course from suggestions
  // -------------------------
  selectCourse(course: any): void {
    this.selectedCourse = course;
    this.course_id = course.id;
    this.courseSearch = course.name;
    this.filteredCourses = [];
  }

  // -------------------------
  // Submit round
  // -------------------------
  submitRound(): void {

    if (!this.course_id || !this.date_played) {
      alert('Please select course and date');
      return;
    }

    this.ws.createManualRound({
      course_id: this.course_id,
      date_played: this.date_played
    }).subscribe({
      next: (res: any) => {

        const roundId = res.round_id;
        this.router.navigate(['/rounds', roundId, 'scores']);

      },
      error: err => {
        console.error(err);
        alert('Failed to create round');
      }
    });

  }

}
