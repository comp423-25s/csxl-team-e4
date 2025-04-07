import { Component, effect, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { SharedModule } from 'src/app/shared/shared.module';
import {
  ActivatedRoute,
  NavigationEnd,
  Router,
  RouterOutlet
} from '@angular/router';

@Component({
  selector: 'app-generate-test',
  standalone: true,
  imports: [
    RouterOutlet,
    SharedModule,
    CommonModule,
    FormsModule,
    MatListModule,
    MatIconModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule
  ],
  templateUrl: './generate-test.component.html',
  styleUrl: './generate-test.component.css'
})
export class GenerateTestComponent {
  constructor(
    private router: Router,
    private route: ActivatedRoute
  ) {
    effect(() => {
      const url = this.router.url;
      this.isResultPage.set(url.endsWith('/result'));
    });

    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.isResultPage.set(this.router.url.endsWith('/result'));
      }
    });
  }

  materials = [
    { timestamp: 'Thursday, 3/27 7:11PM', title: 'Study Guide Unit 2 Topic 3' },
    { timestamp: 'Thursday, 3/27 5:18PM', title: 'Study Guide Unit 2 Topic 4' },
    { timestamp: 'Thursday, 3/27 4:03PM', title: 'Study Guide Unit 2 Topic 1' }
  ];

  inputText = '';
  readonly isResultPage = signal(false);

  goToResultPage() {
    this.router.navigate(['result'], { relativeTo: this.route });
  }
}
