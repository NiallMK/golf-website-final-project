import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { WebserviceService } from '../../services/webservice.service';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-course-detail',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.css']
})
export class CourseComponent implements OnInit {

  course: any;
  images: string[] = [];
  selectedImage: string | null = null;

  openImage(img: string) {
    this.selectedImage = img;
  }

  closeImage() {
    this.selectedImage = null;
  }
  
  constructor(
    private route: ActivatedRoute,
    private webService: WebserviceService
  ) {}

   ngOnInit(): void {

    const id = Number(this.route.snapshot.paramMap.get('id'));

    this.webService.getCourse(id).subscribe({
      next: (data) => {
        this.course = data;
        this.images = data.images || [];
      },
      error: (err) => {
        console.error('Failed to load course', err);
      }
    });

  }
}
