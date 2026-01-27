import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { CoursesComponent } from './components/courses/courses.component';
import { ManualRoundComponent } from './components/manual-round/manual-round.component';
import { ScoreEntryComponent } from './components/score-entry/score-entry.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'courses', component: CoursesComponent },
  { path: 'rounds/new', component: ManualRoundComponent },
  { path: 'rounds/:roundId/scores', component: ScoreEntryComponent}
];
