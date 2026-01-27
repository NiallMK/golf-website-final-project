import { Component, OnInit } from '@angular/core';
import { WebserviceService} from '../../services/webservice.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-courses',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './courses.component.html'
})
export class CoursesComponent implements OnInit {

  courses: any[] = [];

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
