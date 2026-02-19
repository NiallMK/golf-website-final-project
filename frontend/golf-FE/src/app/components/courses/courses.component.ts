import { Component, OnInit } from '@angular/core';
import { WebserviceService} from '../../services/webservice.service';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-courses',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './courses.component.html',
  styleUrls: ['./courses.component.css']
})
export class CoursesComponent implements OnInit {

  courses: any[] = [];
  searchTerm: string = '';

  filteredCourses() {
    return this.courses.filter(course =>
      course.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  constructor(private webService: WebserviceService) {}

  ngOnInit(): void {
    this.webService.getCourses().subscribe({
      next: (data) => {
        console.log('Courses from API:', data);
        this.courses = data;
      },
      error: (err) => {
        console.error('Error loading courses', err);
      }
    });
  }
}
