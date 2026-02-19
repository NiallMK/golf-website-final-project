import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WebserviceService } from '../../services/webservice.service';

@Component({
  selector: 'app-leaderboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './leaderboard.component.html',
  styleUrls: ['./leaderboard.component.css']
})
export class LeaderboardComponent implements OnInit {

  courses: any[] = [];
  leaderboard: any[] = [];
  selectedCourse: number | null = null;

  constructor(private webService: WebserviceService) {}

  ngOnInit(): void {
    this.webService.getCourses().subscribe(data => {
      this.courses = data;
    });
  }

  loadLeaderboard() {
    if (!this.selectedCourse) return;

    this.webService.getCourseLeaderboardById(this.selectedCourse).subscribe(data => {
      this.leaderboard = data;
    });
  }
}
