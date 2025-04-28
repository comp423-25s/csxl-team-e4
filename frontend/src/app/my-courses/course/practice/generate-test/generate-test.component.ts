import { Component } from '@angular/core';
import { Router, ActivatedRoute, RouterOutlet } from '@angular/router';
import { SharedModule } from 'src/app/shared/shared.module';

@Component({
  selector: 'app-generate-test',
  standalone: true,

  imports: [RouterOutlet, SharedModule],
  templateUrl: './generate-test.component.html',
})
export class GenerateTestComponent {
  constructor(
    private router: Router,
    private route: ActivatedRoute
  ) {}

  goToResult(testId: string) {
    const courseId = this.route.snapshot.paramMap.get('course_site_id');
    this.router.navigate([
      `/my-courses/course/${courseId}/practice/generate/result`,
      testId
    ]);
  }
}
