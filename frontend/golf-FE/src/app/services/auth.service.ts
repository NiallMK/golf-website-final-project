import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private BASE_URL = 'http://localhost:5001/api';

  private userSubject = new BehaviorSubject<any | null>(null);
  user$ = this.userSubject.asObservable();

  constructor(private http: HttpClient) {}

  register(name: string, email: string, password: string) {
    return this.http.post<any>(
      `${this.BASE_URL}/auth/register`,
      { name, email, password },
      { withCredentials: true }
    );
  }

  login(email: string, password: string): Observable<any> {
    return this.http.post(
      `${this.BASE_URL}/login`,
      { email, password },
      { withCredentials: true }
    );
  }

  logout(): Observable<any> {
    return this.http.post(
      `${this.BASE_URL}/logout`,
      {},
      { withCredentials: true }
    );
  }

  loadUser() {
    return this.http.get<any>(
      `${this.BASE_URL}/auth/me`,
      { withCredentials: true }
    ).subscribe({
      next: res => this.setUser(res.user),
      error: () => this.clearUser()
    });
  }



  setUser(user: any) {
    this.userSubject.next(user);
  }

  clearUser() {
    this.userSubject.next(null);
  }

  get currentUser() {
    return this.userSubject.value;
  }

  isLoggedIn(): boolean {
    return this.currentUser !== null;
  }

}
