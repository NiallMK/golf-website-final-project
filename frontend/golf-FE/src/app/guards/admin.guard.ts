import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Observable } from 'rxjs';
import { filter, take, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AdminGuard implements CanActivate {

  constructor(
    private auth: AuthService,
    private router: Router
  ) {}

  canActivate(): Observable<boolean> {
    return this.auth.authReady$.pipe(
      filter(ready => ready),   // wait until auth is ready
      take(1),
      map(() => {
        if (this.auth.isAdmin()) {
          return true;
        }

        this.router.navigate(['/']);
        return false;
      })
    );
  }
}