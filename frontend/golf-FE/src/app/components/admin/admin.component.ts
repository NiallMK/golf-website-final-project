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

  editingCourseId: number | null = null;

  course = {
    name: '',
    location: '',
    par: 72,
    course_rating: 72.0,
    slope_rating: 113,
    images: [''],
    latitude: null as number | null,
    longitude: null as number | null,
    description: ''
  };

  courses: any[] = [];
  message = '';

  constructor(private http: HttpClient) {
    this.loadCourses();
    this.loadStats();
    this.loadUsers();
  }

  loadCourses() {
    this.http.get<any[]>(
      `${this.BASE_URL}/courses`,
      { withCredentials: true }
    ).subscribe({
      next: (res) => {
        this.courses = res;
      },
      error: () => {
        this.message = 'Failed to load courses';
      }
    });
  }

  startEdit(course: any) {
    this.editingCourseId = course.id;

    this.course = {
      name: course.name,
      location: course.location,
      par: course.par,
      course_rating: course.course_rating ?? 72,
      slope_rating: course.slope_rating,
      images: course.images?.length ? [...course.images] : [''],
      latitude: course.latitude ?? null,
      longitude: course.longitude ?? null,
      description: course.description ?? ''
    };
  }

  addCourse() {

    if (this.editingCourseId) {
      this.http.put(
        `${this.BASE_URL}/courses/${this.editingCourseId}`,
        this.course,
        { withCredentials: true }
      ).subscribe({
        next: () => {
          this.message = 'Course updated';
          this.editingCourseId = null;
          this.resetForm();
          this.loadCourses();
        },
        error: (err) => {
          this.message = err.error?.error || 'Update failed';
        }
      });

    } else {

      this.http.post(
        `${this.BASE_URL}/courses`,
        this.course,
        { withCredentials: true }
      ).subscribe({
        next: () => {
          this.message = 'Course added successfully';
          this.resetForm();
          this.loadCourses();
        },
        error: (err) => {
          this.message = err.error?.error || 'Error adding course';
        }
      });

    }
  }

  deleteCourse(id: number) {
    if (!confirm('Are you sure you want to delete this course?')) {
      return;
    }

    this.http.delete(
      `${this.BASE_URL}/courses/${id}`,
      { withCredentials: true }
    ).subscribe({
      next: () => {
        this.message = 'Course deleted';
        this.loadCourses();
      },
      error: (err) => {
        this.message = err.error?.error || 'Delete failed';
      }
    });
  }

  addImage() {
    this.course.images.push('');
  }

  removeImage(index: number) {
    this.course.images.splice(index, 1);
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

  
  currentPage = 1;
  itemsPerPage = 5;

  private _searchTerm = '';

  // Prevents error occuring in search even when the letters inserted are correct
  get searchTerm(): string {
    return this._searchTerm;
  }

  set searchTerm(value: string) {
    this._searchTerm = value;
    this.currentPage = 1;
  }

  get filteredCourses() {
    let filtered = this.courses.filter(c =>
      c.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );

    const start = (this.currentPage - 1) * this.itemsPerPage;
    const end = start + this.itemsPerPage;

    return filtered.slice(start, end);
  }

  get totalPages() {
    const filteredCount = this.courses.filter(c =>
      c.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    ).length;

    return Math.ceil(filteredCount / this.itemsPerPage);
  }

  nextPage() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  }

  prevPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }

  users: any[] = [];

  loadUsers() {
    this.http.get<any[]>(
      `${this.BASE_URL}/admin/users`,
      { withCredentials: true }
    ).subscribe({
      next: (res) => {
        this.users = res;
      }
    });
  }

  updateUserRole(user: any) {
    this.http.put(
      `${this.BASE_URL}/admin/users/${user.id}/role`,
      { role: user.role },
      { withCredentials: true }
    ).subscribe({
      next: () => {
        this.message = 'User role updated';
      },
      error: (err) => {
        this.message = err.error?.error || 'Update failed';
      }
    });
  }

  stats: any = null;

  loadStats() {
    this.http.get(
      `${this.BASE_URL}/admin/stats`,
      { withCredentials: true }
    ).subscribe({
      next: (res) => {
        this.stats = res;
      },
      error: () => {
        this.message = 'Failed to load stats';
      }
    });
  }
}