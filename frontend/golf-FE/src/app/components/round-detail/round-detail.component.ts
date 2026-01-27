import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { WebserviceService } from '../../services/webservice.service';

@Component({
  selector: 'app-round-detail',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './round-detail.component.html'
})
export class RoundDetailComponent implements OnInit {

  round: any;
  scores: any[] = [];
  roundId!: number;

  constructor(
    private route: ActivatedRoute,
    private ws: WebserviceService
  ) {}

  ngOnInit(): void {
    this.roundId = Number(this.route.snapshot.paramMap.get('id'));

    this.ws.getRound(this.roundId).subscribe({
      next: data => {
        this.round = data.round;
        this.scores = data.scores;
      },
      error: err => console.error(err)
    });
  }
}
