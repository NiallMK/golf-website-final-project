import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebserviceService {

  private BASE_URL = 'http://127.0.0.1:5001/api';

  constructor(private http: HttpClient) {}

  // --------------------
  // COURSES
  // --------------------
  getCourses(): Observable<any[]> {
    return this.http.get<any[]>(`${this.BASE_URL}/courses`);
  }

  getCourse(id: number): Observable<any> {
    return this.http.get<any>(`${this.BASE_URL}/courses/${id}`);
  }

  getRound(roundId: number) {
    return this.http.get<any>(
      `http://127.0.0.1:5001/api/rounds/${roundId}`
    );
  }

  createManualRound(data: {
    user_id: number;
    course_id: number;
    date_played: string;
  }) {
    return this.http.post(
      'http://127.0.0.1:5001/api/rounds/manual',
      data
    );
  }

  getCourseHoles(courseId: number) {
    return this.http.get<any[]>(
      `http://127.0.0.1:5001/api/courses/${courseId}/holes`
    );
  }

  submitScores(roundId: number, scores: any[]) {
    return this.http.post(
      `http://127.0.0.1:5001/api/rounds/${roundId}/scores`,
      { scores }
    );
  }

  getUser(userId: number) {
    return this.http.get<any>(
      `http://127.0.0.1:5001/api/users/${userId}`
    );
  }

  getUserRounds(userId: number) {
    return this.http.get<any[]>(
      `http://127.0.0.1:5001/api/rounds/user/${userId}`
    );
  }



}
