import { Routes } from '@angular/router';

import { HomeComponent } from './components/home/home.component';
import { CoursesComponent } from './components/courses/courses.component';
import { RecordRoundComponent } from './components/manual-round/record-round.component';
import { ScoreEntryComponent } from './components/score-entry/score-entry.component';
import { MyRoundsComponent } from './components/my-rounds/my-rounds.component';
import { RoundDetailComponent } from './components/round-detail/round-detail.component';
import { ProfileComponent } from './components/profile/profile.component';
import { BookTeeTimeComponent } from './components/book-tee-time/book-tee-time.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';

import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [

  // --------------------
  // Public routes
  // --------------------
  { path: '', component: HomeComponent },
  { path: 'courses', component: CoursesComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },

  // --------------------
  // Protected routes (login required)
  // --------------------
  {
    path: 'rounds/new',
    component: RecordRoundComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'rounds/:roundId/scores',
    component: ScoreEntryComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'rounds',
    component: MyRoundsComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'rounds/:id',
    component: RoundDetailComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'profile',
    component: ProfileComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'book',
    component: BookTeeTimeComponent,
    canActivate: [AuthGuard]
  }

];
