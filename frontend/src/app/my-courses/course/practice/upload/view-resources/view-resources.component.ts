import { Component } from '@angular/core';
import { Router, ActivatedRoute, RouterOutlet } from '@angular/router';
import { SharedModule } from 'src/app/shared/shared.module';

@Component({
  selector: 'app-view-resources',
  standalone: true,
  imports: [SharedModule],
  templateUrl: './view-resources.component.html',
  styleUrl: './view-resources.component.css'
})
export class ViewResourcesComponent {
  constructor(
    private router: Router,
    private route: ActivatedRoute
  ) {}
}
