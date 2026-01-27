import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WebserviceService } from '../../services/webservice.service';

@Component({
  selector: 'app-score-entry',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './score-entry.component.html'
})
export class ScoreEntryComponent implements OnInit {

  roundId!: number;
  courseId!: number;

  holes: any[] = [];
  scores: number[] = [];

  constructor(
    private route: ActivatedRoute,
    private webService: WebserviceService
  ) {}

  ngOnInit(): void {

    // 1️⃣ Get round ID from URL
    this.roundId = Number(this.route.snapshot.paramMap.get('roundId'));

    // 2️⃣ Load round → extract course_id
    this.webService.getRound(this.roundId).subscribe({
      next: (res: any) => {
        console.log('ROUND RESPONSE:', res);

        this.courseId = res.round.course_id;
        console.log('COURSE ID:', this.courseId);

        // 3️⃣ Load holes for course
        this.webService.getCourseHoles(this.courseId).subscribe({
          next: (holes: any[]) => {
            console.log('HOLES:', holes);

            this.holes = holes;
            this.scores = new Array(this.holes.length).fill(null);
          },
          error: err => {
            console.error('Failed to load holes', err);
          }
        });
      },
      error: err => {
        console.error('Failed to load round', err);
      }
    });
  }

  // 4️⃣ Submit scores
  submitScores(): void {

    const payload = this.holes.map((h, i) => ({
      hole_id: h.id,
      strokes: this.scores[i]
    }));

    console.log('SUBMITTING SCORES:', payload);

    this.webService.submitScores(this.roundId, payload).subscribe({
      next: res => {
        alert('Scores submitted successfully!');
        console.log('RESULT:', res);
      },
      error: err => {
        console.error('Failed to submit scores', err);
        alert('Failed to submit scores');
      }
    });
  }

  getTotalScore(): number {
    return this.scores
      .filter(s => s)
      .reduce((sum, s) => sum + Number(s), 0);
  }

}
