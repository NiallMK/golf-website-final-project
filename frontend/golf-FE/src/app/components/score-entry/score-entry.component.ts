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
  scores: (number | null)[] = [];

  constructor(
    private route: ActivatedRoute,
    private webService: WebserviceService
  ) {}

  ngOnInit(): void {

    // Get round ID from URL
    this.roundId = Number(this.route.snapshot.paramMap.get('roundId'));

    // Load round → get course_id
    this.webService.getRound(this.roundId).subscribe({
      next: (res: any) => {
        this.courseId = res.round.course_id;

        // Load holes for this course
        this.webService.getCourseHoles(this.courseId).subscribe({
          next: (holes: any[]) => {
            this.holes = holes;
            this.scores = new Array(this.holes.length).fill(null);
          },
          error: err => console.error('Failed to load holes', err)
        });
      },
      error: err => console.error('Failed to load round', err)
    });
  }

  // Disable submit until every hole has a score
  get allScoresEntered(): boolean {
    return (
      this.scores.length === this.holes.length &&
      this.scores.every(s => s !== null && s > 0)
    );
  }

  // Total score (live)
  get totalScore(): number {
    return this.scores.reduce<number>(
      (sum, s) => sum + (s ?? 0),
      0
    );
  }


  // Front 9 total
  get frontNineTotal(): number {
    return this.holes.reduce((sum, h, i) => {
      return h.hole_number <= 9 ? sum + (this.scores[i] ?? 0) : sum;
    }, 0);
  }

  // Back 9 total
  get backNineTotal(): number {
    return this.holes.reduce((sum, h, i) => {
      return h.hole_number > 9 ? sum + (this.scores[i] ?? 0) : sum;
    }, 0);
  }

  // Submit scores
  submitScores(): void {

    if (!this.allScoresEntered) {
      alert('Please enter a score for every hole');
      return;
    }

    const payload = this.holes.map((h, i) => ({
      hole_id: h.id,
      strokes: this.scores[i]
    }));

    this.webService.submitScores(this.roundId, payload).subscribe({
      next: () => {
        alert('Scores submitted successfully!');
      },
      error: err => {
        console.error('Failed to submit scores', err);
        alert('Failed to submit scores');
      }
    });
  }
}
