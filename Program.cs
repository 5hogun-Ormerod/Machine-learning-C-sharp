using System;
using Accord.Statistics.Kernels;
using Accord.MachineLearning.VectorMachines.Learning;
using Accord.IO;

namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            machine_leanrning_prob problem = new machine_leanrning_prob();

            string path = @"c:\Python\ML\data\train.csv";
            problem.read_from_csv(path, 0);
            Console.WriteLine("Starting the SVM");

            MulticlassSupportVectorLearning<Linear> teacher = new MulticlassSupportVectorLearning<Linear>();
            //MultilabelSupportVectorLearning<Linear> teacher = new MultilabelSupportVectorLearning<Linear>();
            teacher.ParallelOptions.MaxDegreeOfParallelism = 1;
            var machine = teacher.Learn(problem.input_data, problem.output_data);
            Console.WriteLine("Machine trained");
            int[] predicted = machine.Decide(problem.input_data);
            Console.WriteLine("Predicting training output");
            Console.WriteLine("The score for the SVM is {0} %:", 100*problem.score(predicted));
        }

        /*static void char_tree(machine_leanrning_prob prob)
        {
            C45Learning teacher = new C45Learning();
            
            Console.WriteLine("Learning complete");
        }*/

        class machine_leanrning_prob
        {
            /* In this code, we want to define all the variables we have associated with
             * a machine learning problem into one class. 
             *  m is the number of data points to train on
             *  n is the number of features for each data point (dimension of the space)
             *  input_data is an m by n array of doubles that we will initialize in the read_from_csv
             *  output_data is an array of integers of length m representing the class of each 
             *  data is the combination of input and output data
             *  read_from_csv is a method I wrote to take the information from a csv  file at path and
             *  feed it into the above mentioned variables */
            public int m;
            public int n;
            public double[][] input_data;
            public int[] output_data;
            public double[][] data;

            public double score(int[] predicted)
            {
                double sum = 0.0;
                for (int i = 0; i < m; i++)
                {
                    if (predicted[i] == output_data[i])
                    {
                        sum++;
                    }
                }
                return sum / m;
            }

            public void read_from_csv(string path, int outcol)
            {
                /* We will use the Accord framework to grab information from a csv file at path */
                CsvReader csv = new CsvReader(path, true);
                Console.WriteLine("Reading data");
                data = csv.ToJagged<double>();
                m = data.Length;
                n = data[0].Length;
                Console.WriteLine("Reading all {0} lines, each with {1} values.", m, n);
                Console.WriteLine("Takeing column {0} as output.", outcol);
                output_data = new int[m];
                input_data = new double[m][];

                for (int i = 0; i < m; i ++)
                {
                    input_data[i] = new double[n-1];
                    for (int j = 0; j < n-1; j++)
                    {
                        if (j== outcol)
                        {
                            output_data[i] = System.Convert.ToInt16(data[i][j]);
                        }
                        else
                        {
                            if (j < outcol)
                            {
                                input_data[i][j] = data[i][j];
                            }
                            else
                            {
                                input_data[i][j] = data[i][j+1];
                            }
                        }
                    }
                }
            }

            /*public DecisionVariable[] attributes()
            {
                int m = input_data[0].Length;
                DecisionVariable[] att = new DecisionVariable[m];
                for (int i = 0; i < m; i++)
                {
                    att[i] = new DecisionVariable(String.Join("", "data", i.ToString()), DecisionVariableKind.Continuous);
                }
                return att;
            }*/
        }
    }
}
