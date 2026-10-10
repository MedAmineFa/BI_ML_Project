import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-prediction',
  templateUrl: './prediction.component.html',
  styleUrls: ['./prediction.component.css']
})
export class PredictionComponent {
  futurePrediction: number | undefined;
  plotPath: string | undefined;
  predictionError: string | undefined;

  constructor(private http: HttpClient) { }

  predictFuture(): void {
    this.http.get<any>('http://localhost:5000/predict_future')
      .subscribe(
        (response) => {
          this.futurePrediction = response.future_prediction;
          this.predictionError = undefined;
        },
        (error) => {
          this.predictionError = 'Une erreur s\'est produite lors de la prédiction.';
          this.futurePrediction = undefined;
          this.plotPath = undefined;
        }
      );
  }
}
