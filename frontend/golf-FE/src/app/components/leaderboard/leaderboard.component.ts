import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WebserviceService } from '../../services/webservice.service';

@Component({
  selector: 'app-leaderboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './leaderboard.component.html',
  styleUrls: ['./leaderboard.component.css']
})
export class LeaderboardComponent implements OnInit {

  leaderboard: any[] = [];

  constructor(private webService: WebserviceService) {}

  ngOnInit(): void {
    this.webService.getCourseLeaderboard().subscribe({
      next: (data) => {
        this.leaderboard = data;
      },
      error: (err) => {
        console.error('Failed to load leaderboard', err);
      }
    });
  }
}
