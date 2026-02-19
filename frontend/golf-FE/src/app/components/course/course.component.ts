import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { GoogleMapsModule } from '@angular/google-maps';
import { WebserviceService } from '../../services/webservice.service';

@Component({
  selector: 'app-course-detail',
  standalone: true,
  imports: [CommonModule, RouterModule, GoogleMapsModule],
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.css']
})
export class CourseComponent implements OnInit {

  course: any;

  center: google.maps.LatLngLiteral = { lat: 0, lng: 0 };
  zoom = 14;

  images: string[] = [];
  selectedImage: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private webService: WebserviceService
  ) {}

  ngOnInit(): void {

    const id = Number(this.route.snapshot.paramMap.get('id'));

    this.webService.getCourse(id).subscribe((data) => {

      console.log("API response:", data);

      this.course = data;
      this.images = data.images || [];

      // Force numbers
      const lat = parseFloat(data.latitude);
      const lng = parseFloat(data.longitude);

      console.log("Parsed lat/lng:", lat, lng);

      if (!isNaN(lat) && !isNaN(lng)) {
        this.center = { lat, lng };
      }

    });

  }

  openImage(img: string): void {
    this.selectedImage = img;
  }

  closeImage(): void {
    this.selectedImage = null;
  }
}
