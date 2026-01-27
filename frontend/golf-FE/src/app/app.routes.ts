import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { CoursesComponent } from './components/courses/courses.component';
import { RecordRoundComponent } from './components/manual-round/record-round.component';
import { ScoreEntryComponent } from './components/score-entry/score-entry.component';
import { MyRoundsComponent } from './components/my-rounds/my-rounds.component';
import { RoundDetailComponent } from './components/round-detail/round-detail.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'courses', component: CoursesComponent },
  { path: 'rounds/new', component: RecordRoundComponent },
  { path: 'rounds/:roundId/scores', component: ScoreEntryComponent},
  { path: 'rounds', component: MyRoundsComponent},
  { path: 'rounds/:id', component: RoundDetailComponent}

];
