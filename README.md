# medNodeAnalysis

<p>This project uses the dataset found <a href="https://www.w3schools.com">here</a>, published as part of the following article:</br>
<em>I. Giotis, N. Molders, S. Land, M. Biehl, M.F. Jonkman and N. Petkov: "MED-NODE: A computer-assisted melanoma diagnosis system using non-dermoscopic images", Expert Systems with Applications, 42 (2015), 6578-6585 </em></br>It was realised as a project necessary for the first term class of Physiology in M.Sc. in Medical Informatics, A.U.TH., for the classification, by using ML, to superficially spreading melanomas and naevi. </p>
<p>The first method is random forest classification, according to six parametres of every photo. Each photo was read using python and OpenCV <em>(code <a href="https://github.com/JungleHippo/medNodeAnalysis/blob/master/NumericalDataExtraction.py">here</a>)</em>, had the normalized numbers of pixels of a given color value in every one of RGB channels counted and saved as cumulative distribution curves in <a href="https://github.com/JungleHippo/medNodeAnalysis/blob/master/PixelIntensitiesHistogramsandCDFs.zip">*.csv files</a>, in the form of:
  <table>
    <tr>
      <th>Color Intensity</th>
      <th>Photo 1</th>
      <th>Photo 2</th>
      <th>...</th>
      <th>Photo 170</th>
    </tr>
    <tr>
      <td>0</td>
      <td>f<sub>0,1</sub></td>
      <td>f<sub>0,2</sub></td>
      <td>...</td>
      <td>f<sub>0,170</sub></td>
    </tr>
    <tr>
      <td>1</td>
      <td>f<sub>1,1</sub></td>
      <td>f<sub>1,2</sub></td>
      <td>...</td>
      <td>f<sub>1,170</sub></td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>255</td>
      <td>f<sub>255,1</sub></td>
      <td>f<sub>255,2</sub></td>
      <td>...</td>
      <td>f<sub>255,170</sub></td>
    </tr>
  </table></p>
<p>The .csv files were the read with R and for every photo and color, logistic curves were fitted, resulting in 3 parametres, scale, asymptote and xmid, with the formula <em>y = Asym/(1-exp((x-xmid)/scal))</em>. The asymptotes and scales were used for each photo, resulting to 6 predictors from the 3 colors, used to train a random forest ML model. The code for the training is located in the <em>RandomForest</em> folder. </p>
<p>The description for the second method will be soon available.</p>
    
