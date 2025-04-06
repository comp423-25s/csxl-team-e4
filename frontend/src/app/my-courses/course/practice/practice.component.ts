import { Component } from '@angular/core';
import { PracticeCardComponent } from './widgets/practice-card/practice-card.widget';
import { SharedModule } from "../../../shared/shared.module";
import { MatCardModule } from '@angular/material/card';


@Component({
  selector: 'app-practice',
  standalone: true,
  imports: [PracticeCardComponent,MatCardModule,  SharedModule],
  templateUrl: './practice.component.html',
  styleUrl: './practice.component.css'
})
export class PracticeComponent {
  /** Route information to be used in the routing module */
  public static Route = {
    path: 'practice',
    title: 'course',
    component: PracticeComponent
  };
}
