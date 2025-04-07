import { Component } from '@angular/core';
import { PracticeCardComponent } from './widgets/practice-card/practice-card.widget';
import { SharedModule } from '../../../shared/shared.module';
import { MatCardModule } from '@angular/material/card';
import { Router, ActivatedRoute, RouterModule } from '@angular/router';
import { GenerateTestComponent } from './generate-test/generate-test.component';
import { MatDividerModule } from '@angular/material/divider';




@Component({
  selector: 'app-practice',
  standalone: true,
  imports: [PracticeCardComponent, MatCardModule, SharedModule, RouterModule, MatDividerModule],
  templateUrl: './practice.component.html',
  styleUrl: './practice.component.css'
})
export class PracticeComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'practice',
    title: 'course',
    component: PracticeComponent,
    children: [
      {
        path: 'generate',
        component: GenerateTestComponent
      }
    ]
  };

  constructor(
    private router: Router,
    private route: ActivatedRoute
  ) {}

  goToGenerateTest() {
    this.router.navigate(['generate'], { relativeTo: this.route });
  }
}
