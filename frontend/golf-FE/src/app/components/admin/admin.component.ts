import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent {

  private BASE_URL = 'http://localhost:5001/api';

  course = {
    name: '',
    location: '',
    par: 72,
    course_rating: 72.0,
    slope_rating: 113,
    images: [''],
    latitude: null,
    longitude: null,
    description: ''
  };

  message = '';

  constructor(private http: HttpClient) {}

  addCourse() {
    this.http.post(
      `${this.BASE_URL}/courses`,
      this.course,
      { withCredentials: true }
    ).subscribe({
      next: () => {
        this.message = 'Course added successfully!';
        this.resetForm();
      },
      error: (err) => {
        this.message = err.error?.error || 'Error adding course';
      }
    });
  }

  resetForm() {
    this.course = {
      name: '',
      location: '',
      par: 72,
      course_rating: 72.0,
      slope_rating: 113,
      images: [''],
      latitude: null,
      longitude: null,
      description: ''
    };
  }

  addImage() {
    this.course.images.push('');
  }

  removeImage(index: number) {
    this.course.images.splice(index, 1);
  }
}