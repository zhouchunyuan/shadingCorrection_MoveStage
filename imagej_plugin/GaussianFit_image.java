// modified according to http://commons.apache.org/proper/commons-math/userguide/leastsquares.html
import ij.*;
import ij.process.*;
import ij.gui.*;
import java.awt.*;
import ij.plugin.*;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import org.apache.commons.math3.geometry.euclidean.twod.Vector2D;
import org.apache.commons.math3.util.*;
import org.apache.commons.math3.linear.*;
import java.util.Arrays;
import java.io.*;

import org.apache.commons.math3.fitting.leastsquares.*;
import javax.swing.*;

public class GaussianFit_image implements PlugIn {
        ///////// param////////////
        RealMatrix pixArray;

        public void showit(double amp,double x0, double y0, double sigma) {
            int width = 512;
            int height = 512;
            ImageProcessor ip = new ShortProcessor(width, height);
            for (int j=0;j<height;j++) {
                for (int i=0;i<width;i++) {
                    double v = amp*Math.exp(-(((double)i/width-x0)*((double)i/width-x0)+((double)j/height-y0)*((double)j/height-y0))/(sigma*sigma));
                    ip.putPixel(i,j,(int)v);
                }
            }
            ImagePlus imp = new ImagePlus("Shading Image", ip);
            imp.show();
        }


        public String readFile(String filename) {
            String content = null;
            File file = new File(filename); // For example, foo.txt
            FileReader reader = null;
            try {
                reader = new FileReader(file);
                char[] chars = new char[(int) file.length()];
                reader.read(chars);
                content = new String(chars);
                reader.close();
            } catch (IOException e) {
                e.printStackTrace();
            }

            StringBuilder sb = new StringBuilder(content.length());
            for (int i = 0; i < content.length(); i++) {
                char ch = content.charAt(i);
                if (ch > 0) {
                    sb.append(ch);
                }
            }
            return sb.toString();
        }

        // main()
        public void run(String arg) {

            ///////////////////////////////////
            JFileChooser fc = new JFileChooser();
            fc.setDialogTitle("Open ShadingSample.txt");
            int returnVal = fc.showOpenDialog(IJ.getApplet());

            String dataString = readFile(fc.getSelectedFile().getPath());
            String dataLines[] = dataString.split("\n");

            pixArray = new Array2DRowRealMatrix(dataLines.length, 3);
            for (int i=0;i<dataLines.length;i++) {
                String s[] = dataLines[i].split(",");
                pixArray.setEntry(i,0,Double.parseDouble(s[0]));
                pixArray.setEntry(i,1,Double.parseDouble(s[1]));
                pixArray.setEntry(i,2,Double.parseDouble(s[2]));
            }
            ////////////////////////////////////////
            // the model function is gaussian distribution,
            // the parameters are estimated from txt file by NIS-Elements
            MultivariateJacobianFunction GaussianIntensity = new MultivariateJacobianFunction() {
                public Pair<RealVector, RealMatrix> value(final RealVector param) {
                    double amp = param.getEntry(0);
                    double x0 = param.getEntry(1);
                    double y0 = param.getEntry(2);
                    double sigma = param.getEntry(3);

                    RealVector value = new ArrayRealVector(pixArray.getRowDimension());
                    RealMatrix jacobian = new Array2DRowRealMatrix(pixArray.getRowDimension(), 4);

                    for (int i = 0; i < pixArray.getRowDimension(); ++i) {

                        double x = pixArray.getEntry(i,0);
                        double y = pixArray.getEntry(i,1);

                        double modelI = amp*Math.exp(-((x-x0)*(x-x0)+(y-y0)*(y-y0))/(sigma*sigma));

                        value.setEntry(i,modelI);
                        // derivative with respect to p0 = x center
                        jacobian.setEntry(i, 0, modelI/amp);
                        jacobian.setEntry(i, 1, modelI*2*(x-x0));
                        jacobian.setEntry(i, 2, modelI*2*(y-y0));
                        jacobian.setEntry(i, 3, modelI*2*((x-x0)*(x-x0)+(y-y0)*(y-y0))/(sigma*sigma*sigma));

                    }

                    return new Pair<RealVector, RealMatrix>(value, jacobian);

                }
            };

            //
            double maxIntensity = 0.0;
            double xc=0.0,yc=0.0,sum = 0.0;//weighted center
            double sigma_ = 0.5;//fix to half of width
            // the target is intensity for each point, read from txt file
            // maxIntensity,xc,yc,sigma_   are used as initial guess
            double[] prescribedGuassian = new double[pixArray.getRowDimension()];
            for (int i = 0; i < pixArray.getRowDimension(); ++i) {
                double x = pixArray.getEntry(i,0);
                double y = pixArray.getEntry(i,1);
                double v = pixArray.getEntry(i,2);
                prescribedGuassian[i]= v;
                if (maxIntensity < v)maxIntensity=v;
                xc += v*x;
                yc += v*y;
                sum +=v;
            }
            xc = xc/sum;
            yc = yc/sum;

            // least squares problem to solve : modeled radius should be close to target radius
            LeastSquaresProblem problem = new LeastSquaresBuilder().
            start(new double[] { maxIntensity,xc,yc,sigma_}).
            model(GaussianIntensity).
            target(prescribedGuassian).
            lazyEvaluation(false).
            maxEvaluations(1000).
            maxIterations(1000).
            build();
            LeastSquaresOptimizer.Optimum optimum = new LevenbergMarquardtOptimizer().optimize(problem);
            RealVector ans = new ArrayRealVector(new double[] {
                optimum.getPoint().getEntry(0),
                optimum.getPoint().getEntry(1),
                optimum.getPoint().getEntry(2),
                optimum.getPoint().getEntry(3)
            });

            showit(optimum.getPoint().getEntry(0),
                   optimum.getPoint().getEntry(1),
                   optimum.getPoint().getEntry(2),
                   optimum.getPoint().getEntry(3));

            IJ.log("amp="+optimum.getPoint().getEntry(0)+
                   " | X0="+optimum.getPoint().getEntry(1)+
                   " | y0="+optimum.getPoint().getEntry(2)+
                   " | sigma="+optimum.getPoint().getEntry(3));
            IJ.log("RMS: "           + optimum.getRMS());
            IJ.log("evaluations: "   + optimum.getEvaluations());
            IJ.log("iterations: "    + optimum.getIterations());
        }

}
