import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { SharedModule } from '../../../shared/shared.module';
import { PracticeCardComponent } from './widgets/practice-card/practice-card.widget';
import { GenerateTestComponent } from './generate-test/generate-test.component';

@Component({
  selector: 'app-practice',
  standalone: true,
  imports: [
    PracticeCardComponent,
    MatCardModule,
    SharedModule,
    RouterModule,
    MatDividerModule
  ],
  templateUrl: './practice.component.html',
  styleUrl: './practice.component.css'
})
export class PracticeComponent implements OnInit {
  /** Route information to be used in the routing module */

  isInsideGenerate = false;

  constructor(
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.isInsideGenerate = this.router.url.includes('/practice/generate');
    this.router.events.subscribe(() => {
      this.isInsideGenerate = this.router.url.includes('/practice/generate');
    });
  }

  goToGenerateTest() {
    this.router.navigate(['generate'], { relativeTo: this.route });
  }
  goToUpload() {
    this.router.navigate(['upload'], { relativeTo: this.route });
  }
}
