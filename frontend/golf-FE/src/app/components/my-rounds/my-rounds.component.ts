import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { WebserviceService } from '../../services/webservice.service';

@Component({
  selector: 'app-my-rounds',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './my-rounds.component.html'
})
export class MyRoundsComponent implements OnInit {

  rounds: any[] = [];

  // TEMP: until auth
  user_id = 1;

  constructor(private ws: WebserviceService) {}

  ngOnInit(): void {
    this.ws.getUserRounds(this.user_id).subscribe({
      next: data => this.rounds = data,
      error: err => console.error(err)
    });
  }
}
