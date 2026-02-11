import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { WebserviceService } from '../../services/webservice.service';

@Component({
  selector: 'app-my-rounds',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './my-rounds.component.html',
  styleUrls: ['./my-rounds.component.css']
})
export class MyRoundsComponent implements OnInit {

  rounds: any[] = [];

  constructor(
    private ws: WebserviceService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.ws.getUserRounds().subscribe({
      next: data => this.rounds = data,
      error: err => {
        if (err.status === 401) {
          this.router.navigate(['/login']);
        }
      }
    });
  }

}
