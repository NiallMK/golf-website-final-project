import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { NavbarComponent } from './components/navbar/navbar.component';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterModule,        
    NavbarComponent
  ],
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {

  constructor(private auth: AuthService) {}

  ngOnInit(): void {
    this.auth.loadUser();
  }
}
