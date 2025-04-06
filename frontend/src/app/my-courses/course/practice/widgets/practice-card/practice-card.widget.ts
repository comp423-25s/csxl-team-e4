import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { Input } from '@angular/core';
import { RouterModule } from '@angular/router';
import { EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-practice-card',
  standalone: true,
  imports: [MatCardModule, MatButtonModule, RouterModule],
  templateUrl: './practice-card.widget.html',
  styleUrl: './practice-card.widget.scss'
})
export class PracticeCardComponent {
  @Input() title!: string;
  @Input() description!: string;
  @Input() buttonLabel!: string;
  @Input() buttonRoute!: string;

  @Output() clicked = new EventEmitter<void>();
}
