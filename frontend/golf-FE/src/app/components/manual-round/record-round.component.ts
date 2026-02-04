import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WebserviceService } from '../../services/webservice.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-manual-round',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './record-round.component.html',
  styleUrls: ['./record-round.component.css']
})
export class RecordRoundComponent implements OnInit {

  courses: any[] = [];
  course_id: number | null = null;
  date_played: string = '';

  // TEMP: simulated logged-in user
  user_id = 1;

  constructor(private webService: WebserviceService, private router: Router) {}

  ngOnInit(): void {
    this.webService.getCourses().subscribe({
      next: (data) => this.courses = data,
      error: (err) => console.error(err)
    });
  }

  submitRound() {
    if (!this.course_id || !this.date_played) {
      alert('Please select a course and date');
      return;
    }
    
    this.webService.createManualRound({
      user_id: this.user_id,
      course_id: this.course_id,
      date_played: this.date_played
    }).subscribe({
      next: (res: any) => {
        alert('Round created successfully');
        this.router.navigate([`/rounds/${res.round_id}/scores`]);
      },
      error: () => alert('Failed to create round')
    });

  }

  courseSearch: string = '';
  filteredCourses: any[] = [];

  filterCourses() {
    if (!this.courseSearch) {
      this.filteredCourses = [];
      return;
    }

    const search = this.courseSearch.toLowerCase();

    this.filteredCourses = this.courses
      .filter(c => c.name.toLowerCase().includes(search))
      .slice(0, 6); // limit suggestions
  }

  selectCourse(course: any) {
    this.course_id = course.id;
    this.courseSearch = course.name;
    this.filteredCourses = [];
  }

}
