import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebserviceService {

  private BASE_URL = 'http://localhost:5001/api';

  constructor(private http: HttpClient) {}

  // --------------------
  // COURSES (PUBLIC)
  // --------------------
  getCourses(): Observable<any[]> {
    return this.http.get<any[]>(`${this.BASE_URL}/courses`);
  }

  getCourse(id: number): Observable<any> {
    return this.http.get<any>(`${this.BASE_URL}/courses/${id}`);
  }

  getCourseHoles(courseId: number) {
    return this.http.get<any[]>(
      `${this.BASE_URL}/courses/${courseId}/holes`
    );
  }

  // --------------------
  // ROUNDS (AUTH)
  // --------------------
  getRound(roundId: number) {
    return this.http.get<any>(
      `${this.BASE_URL}/rounds/${roundId}`,
      { withCredentials: true }
    );
  }

  createManualRound(data: {
    course_id: number;
    date_played: string;
  }) {
    return this.http.post(
      `${this.BASE_URL}/rounds/manual`,
      data,
      { withCredentials: true }
    );
  }

  submitScores(roundId: number, scores: any[]) {
    return this.http.post(
      `${this.BASE_URL}/rounds/${roundId}/scores`,
      { scores },
      { withCredentials: true }
    );
  }

  getUserRounds() {
    return this.http.get<any[]>(
      `${this.BASE_URL}/rounds`,
      { withCredentials: true }
    );
  }

  getCourseLeaderboard() {
    return this.http.get<any[]>(
      `${this.BASE_URL}/leaderboard/courses`
    );
  }


  // --------------------
  // USER / PROFILE (AUTH)
  // --------------------
  getUserProfile() {
    return this.http.get<any>(
      `${this.BASE_URL}/users/profile`,
      { withCredentials: true }
    );
  }

  recalculateHandicap() {
    return this.http.post(
      `${this.BASE_URL}/handicap/recalculate`,
      {},
      { withCredentials: true }
    );
  }


  getHandicapHistory() {
    return this.http.get<any[]>(
      `${this.BASE_URL}/handicap/history`,
      { withCredentials: true }
    );
  }

  // --------------------
  // BOOKINGS
  // --------------------
  getAvailableTeeTimes(courseId: number, date: string) {
    return this.http.get<any[]>(
      `${this.BASE_URL}/teetimes/available?course_id=${courseId}&date=${date}`
    );
  }

  bookTeeTime(teeTimeId: number) {
    return this.http.post(
      `${this.BASE_URL}/bookings`,
      { teetime_id: teeTimeId },
      { withCredentials: true }
    );
  }

  getUserBookings() {
    return this.http.get<any[]>(
      `${this.BASE_URL}/bookings`,
      { withCredentials: true }
    );
  }


  cancelBooking(bookingId: number) {
    return this.http.delete(
      `${this.BASE_URL}/bookings/${bookingId}`,
      { withCredentials: true }
    );
  }

}
