import { Component } from '@angular/core';
import { AppService } from './app.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  title = 'chatbot';
  chatVisibleFlag: boolean;
  chatIconName: string;
  titleButtonName: string;

  constructor(private appService: AppService) {
    this.chatVisibleFlag = true;
    this.chatIconName = 'insights';
    this.titleButtonName = '  Statistics';
  }
}
