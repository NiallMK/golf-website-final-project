import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Observable } from 'rxjs';
import { map, take } from 'rxjs/operators';
import { filter} from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private auth: AuthService, private router: Router) {}

  canActivate(): Observable<boolean> {
    return this.auth.authReady$.pipe(
      filter(ready => ready === true),
      take(1),
      map(() => {
        if (this.auth.currentUser) {
          return true;
        }

        this.router.navigate(['/login']);
        return false;
      })
    );
  }

}
