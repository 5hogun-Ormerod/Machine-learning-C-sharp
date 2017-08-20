/* Author: Christopher Michael Ormerod */



using System;
using System.Collections;
using System.Linq;
using System.Data;
using Accord.Statistics.Kernels;
using Accord.MachineLearning.VectorMachines.Learning;
using Accord.MachineLearning.DecisionTrees;
using Accord.MachineLearning.DecisionTrees.Learning;
using Accord.MachineLearning;
using Accord.Statistics.Filters;
using Accord.IO;
using Alea;
using System.Collections.Generic;

namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            machine_learning_prob problem = new machine_learning_prob();
            
            string path = @"c:\Python\ML\data\train.csv";
            problem.read_from_csv(path, "label");
            /*problem.drop("ID");
            problem.drop("year");
            problem.drop("hispanic");
            problem.drop("police");
            problem.Select_feature_geq("age", 15);
            problem.Select_feature_leq("age", 60);
            problem.Describe_data();
            problem.Select_target_categorical(new string[] { "Homocide", "Suicide" });*/
            problem.Describe_data();
            LinearSVM(ref problem);
        }

        ///<summary>
        ///<para>This class contains methods used for data manipulation and cleaning</para>
        ///</summary>
        public class machine_learning_prob
        {
            /* In this code, we want to define all the variables we have associated with
             * a machine learning problem into one class. 
             *  number_of_items is the number of data points to train on
             *  number_of_features is the number of features for each data point (dimension of the space)
             *  input_array is array of doubles that we will initialize in the read_from_csv
             *  output_array is an array of integers of length m representing the class of each 
             *  data is the combination of input and output data
             *  read_from_csv is a method I wrote to take the information from a csv  file at path and
             *  feed it into the above mentioned variables */
            public int number_of_features =0;
            public int number_of_items=0;
            public string[] features;
            public string target;
            public string[] target_classes;
            public double[][] input_array;
            public int dim;
            private DataTable data_table;
            public string[][] feature_classes; /* this is an array of integers: 1 if feature i is continuous, 
                                                the number of classes of feature i if discrete */ 
            public int[] output_array;
            public Type[] feature_type;
            public bool[][] output_class_table;

            public double[][] test_array = null;
            public int[] test_output_values = null;


            ///<summary>
            ///<para>This method parses a csv file into the public variables of the class</para>
            ///<para>Warning: needs all values present</para>
            ///</summary>
            public void read_from_csv(string path, string col)
            {
                /* We will use the Accord framework to grab information from a csv file at path */
                CsvReader csv = new CsvReader(path, hasHeaders: true);
                data_table = csv.ToTable();
                number_of_features = data_table.Columns.Count-1;
                number_of_items = data_table.Rows.Count;
                features = new string[number_of_features];
                feature_type = new Type[number_of_features];
                feature_classes = new string[number_of_features][];
                output_class_table = new bool[number_of_items][];
                int offset = 0;
                for (int i = 0; i < data_table.Columns.Count; i++)
                {
                    if (col != data_table.Columns[i].ToString())
                    {
                        features[i - offset] = data_table.Columns[i].ToString();
                        double value;
                        /* We now determine whether the column holds string values or
                         * double values by trying to Parse to a double */
                        if (double.TryParse(data_table.Rows[0][data_table.Columns[i]].ToString(), out value))
                        {
                            feature_type[i - offset] = typeof(double);
                            feature_classes[i - offset] = new string[] { "" };
                            //Console.WriteLine("Entries for feature {0} added.", i - offset);
                        }
                        else
                        {
                            feature_type[i - offset] = typeof(string);
                            HashSet<string> values = new HashSet<string>();
                            foreach (DataRow row in data_table.Rows)
                            {
                                values.Add(row[data_table.Columns[i]].ToString());
                            }
                            feature_classes[i - offset] = values.ToArray<string>();
                            //Console.WriteLine("Entries for feature {0} added.", i - offset);
                        }
                    }
                    else
                    {
                        offset = 1;
                        target = data_table.Columns[i].ToString();
                        HashSet<string> values = new HashSet<string>();
                        foreach (DataRow row in data_table.Rows)
                        {
                            values.Add(row[target].ToString());
                        }
                        target_classes = values.ToArray<string>();
                    }
                }
                load_data_from_table();
            }

            ///<summary>
            ///<para>This method normalizes a continuous feature so that the resulting variables are between 0 and 1</para>
            ///</summary>
            public void normalize_feature(string feature_name)
            {

            }

            public void drop(string feature_name)
            {
                int feature_number = Array.IndexOf(features, feature_name);
                drop(feature_number);
            }

            public void drop(int feature_number)
            {
                //Console.WriteLine("Dropping feature {0}", features[feature_number]);
                double[][] new_input_array = new double[number_of_items][];
                int new_dim = dim - feature_classes[feature_number].Length;
                string[] new_features = new string[number_of_features - 1];
                string[][] new_feature_classes = new string[number_of_features - 1][];
                Type[] new_feature_types = new Type[number_of_features - 1];
                int feature_offset = 0;
                for (int i = 0;i< number_of_features;i++)
                {
                    if (i!= feature_number)
                    {
                        new_features[feature_offset] = features[i];
                        new_feature_types[feature_offset] = feature_type[i];
                        new_feature_classes[feature_offset] = new string[feature_classes[i].Length];
                        Array.Copy(feature_classes[i], new_feature_classes[feature_offset],feature_classes[i].Length);
                        feature_offset += 1;
                    }
                }
                //Console.WriteLine("new dimension is {0}",new_dim);
                for (int i = 0; i < number_of_items;i++)
                {
                    new_input_array[i] = new double[new_dim];
                    int new_offset = 0;
                    int old_offset = 0;
                    for (int j=0; j< number_of_features; j++)
                    {
                        if (j != feature_number)
                        {
                            for (int k=0;k<feature_classes[j].Length;k++)
                            {
                                new_input_array[i][new_offset] = input_array[i][old_offset];
                                { new_offset += 1; old_offset += 1; }
                            }
                        }
                        else { old_offset += feature_classes[j].Length; }
                    }
                }
                dim = new_dim;
                input_array = new_input_array;
                number_of_features -= 1;
                features = new_features;
                feature_type = new_feature_types;
                feature_classes = new_feature_classes;
            }

            public machine_learning_prob Copy()
            {
                machine_learning_prob problem = new machine_learning_prob();
                problem.dim = dim;
                problem.number_of_features = number_of_features;
                problem.number_of_items = number_of_items;
                problem.target = target;
                problem.target_classes = new string[target_classes.Length];
                problem.features = new string[number_of_features];
                problem.input_array = new double[number_of_items][];
                problem.output_array = new int[number_of_items];
                problem.feature_classes = new string[number_of_features][];
                Array.Copy(target_classes, problem.target_classes,target_classes.Length);
                Array.Copy(output_array, problem.output_array, number_of_items);
                Array.Copy(features, problem.features, number_of_features);
                for (int k = 0; k < number_of_features; k++)
                {
                    problem.feature_classes[k] = new string[feature_classes[k].Length];
                    Array.Copy(feature_classes[k],problem.feature_classes[k], feature_classes[k].Length);
                }
                for (int i=0;i< number_of_items;i++)
                {
                    problem.input_array[i] = new double[dim];
                    Array.Copy(input_array[i], problem.input_array[i], dim);
                }
                return problem;
            }

            public void test_train_split(double p)
            {
                /* We assume that 0 <p < 1 */
                int new_number_of_items = System.Convert.ToInt32(Math.Round(System.Convert.ToDouble(number_of_items) * p));
                int number_of_test_items = number_of_items - new_number_of_items;

                Random generator = new Random();
                List<double[]> test_list = new List<double[]>();
                List<int> test_output_list = new List<int>();
                List<int> entries = new List<int>();
                for (int i=0;i < number_of_items;i++) { entries.Add(i); }
                for (int i =0;i< number_of_test_items;i++)
                {
                    int random_index = entries[generator.Next(0, entries.Count-1)];
                    test_output_list.Add(output_array[random_index]);
                    test_list.Add(input_array[random_index]);
                    entries.Remove(random_index);
                }
                test_array = test_list.ToArray<double[]>();
                test_output_values = test_output_list.ToArray<int>();
                Select_subset(entries.ToArray<int>());
            }

            private void load_data_from_table()
            {
                /* this method is meant to fill the arrays input_data and output_data
                 * from the above loaded data table, given the data in data_table
                 * and the feature types found above */
                dim = 0;
                for (int i= 0;i < number_of_features;i++) { dim = dim+ feature_classes[i].Length; }
                Console.WriteLine("Dimension of the aggregated data is {0}", dim);
                input_array = new double[number_of_items][];
                output_array = new int[number_of_items];
                for (int i = 0; i < number_of_items; i++)
                {
                    input_array[i] = new double[dim];
                    int offset_col = 0;
                    int offset_dim = 0;
                    for (int j=0;j< data_table.Columns.Count;j++)
                    {
                        if (target != data_table.Columns[j].ToString() )
                        {
                            if (feature_type[j-offset_col]==typeof(double))
                            {
                                input_array[i][offset_dim] = double.Parse(data_table.Rows[i][j].ToString());
                                offset_dim+= 1;
                            }
                            else
                            {
                                for (int k=0;k<feature_classes[j-offset_col].Length;k++)
                                {
                                    if (feature_classes[j - offset_col][k]==data_table.Rows[i][j].ToString())
                                    { input_array[i][offset_dim] = 1; }
                                    else { input_array[i][offset_dim] = 0; }
                                    offset_dim += 1;
                                }
                            }
                        }
                        else
                        {
                            offset_col = 1;
                            output_array[i] = Array.IndexOf(target_classes, data_table.Rows[i][j].ToString());
                        }
                    }
                }
            }

            public void Select_feature_geq(string feature_name, double value)
            {
                int feature_index = Array.IndexOf(features, feature_name);
                int feature_position = 0;
                for (int i=0;i < feature_index;i++) { feature_position += feature_classes[i].Length; }
                if (feature_type[feature_index] == typeof(double))
                {
                    List<int> entries = new List<int>();
                    for (int i = 0; i < number_of_items; i++)
                    {
                        if (input_array[i][feature_position] >= value)
                        {
                            entries.Add(i);
                        }
                    }
                    int new_number_of_items = entries.ToArray().Length;
                    if (new_number_of_items == 0)
                    {
                        Console.WriteLine("Selection is Empty");
                    }
                    else
                    {
                        double[][] new_input_array = new double[new_number_of_items][];
                        int[] new_output_array = new int[new_number_of_items];
                        for (int i =0;i < new_number_of_items;i++)
                        {
                            new_input_array[i] = new double[dim];
                            Array.Copy(input_array[entries[i]], new_input_array[i], dim);
                            new_output_array[i] = output_array[entries[i]];
                        }
                        number_of_items = new_number_of_items;
                        input_array = new_input_array;
                        output_array = new_output_array;
                    }
                }
                else { Console.WriteLine("Invalid selection, type is categorical"); }
            }

            public void Select_feature_categorical(string feature_name, string value)
            {
                Select_feature_categorical(feature_name, new string[] { value });
            }

            public void Select_feature_categorical(string feature_name, string[] values)
            {
                int feature_index = Array.IndexOf(features, feature_name);
                int feature_position = 0;
                for (int i = 0; i < feature_index; i++) { feature_position += feature_classes[i].Length; }
                //Console.WriteLine("I got here, {0}", feature_position);
                if (feature_type[feature_index] == typeof(string))
                {
                    List<int> entries = new List<int>();
                    for (int i = 0; i < number_of_items; i++)
                    {
                        bool accept = false;
                        for (int k = 0; k < values.Length;k++)
                        {
                            int sub_index = Array.IndexOf(feature_classes[feature_index], values[k]);
                            if (input_array[i][feature_position+sub_index] == 1) { accept = true;  }
                        }
                        if (accept==true)
                        {
                            entries.Add(i);
                        }
                    }
                    Select_subset(entries.ToArray());                    
                }
                else
                {
                    Console.WriteLine("Invalid selection");
                }
            }

            public void Select_target_categorical(string[] values)
            {
                List<int> entries = new List<int>();
                HashSet<string> val_set = new HashSet<string>(values);
                for (int i=0; i< number_of_items;i++)
                {
                    bool accept = val_set.Contains(target_classes[output_array[i]]);
                    if (accept==true)
                    {
                        entries.Add(i);
                    }
                }
                Select_subset(entries.ToArray());
            }

            private void Select_subset(int[] entries)
            {
                int new_number_of_items = entries.ToArray().Length;
                double[][] new_input_array = new double[new_number_of_items][];
                int[] new_output_array = new int[new_number_of_items];
                for (int i = 0; i < new_number_of_items; i++)
                {
                    new_input_array[i] = new double[dim];
                    Array.Copy(input_array[entries[i]], new_input_array[i], dim);
                    new_output_array[i] = output_array[entries[i]];
                }
                number_of_items = new_number_of_items;
                input_array = new_input_array;
                output_array = new_output_array;
            }

            public void Select_feature_leq(string feature_name, double value)
            {
                int feature_index = Array.IndexOf(features, feature_name);
                int feature_position = 0;
                for (int i = 0; i < feature_index; i++) { feature_position += feature_classes[i].Length; }
                if (feature_type[feature_index] == typeof(double))
                {
                    List<int> entries = new List<int>();
                    for (int i = 0; i < number_of_items; i++)
                    {
                        if (input_array[i][feature_position] <= value)
                        {
                            entries.Add(i);
                        }
                    }
                    int new_number_of_items = entries.ToArray().Length;
                    if (new_number_of_items == 0)
                    {
                        Console.WriteLine("Selection is Empty");
                    }
                    else
                    {
                        double[][] new_input_array = new double[new_number_of_items][];
                        int[] new_output_array = new int[new_number_of_items];
                        for (int i = 0; i < new_number_of_items; i++)
                        {
                            new_input_array[i] = new double[dim];
                            Array.Copy(input_array[entries[i]], new_input_array[i], dim);
                            new_output_array[i] = output_array[entries[i]];
                        }
                        number_of_items = new_number_of_items;
                        input_array = new_input_array;
                        output_array = new_output_array;
                    }
                }
                else { Console.WriteLine("Invalid selection, type is categorical"); }
            }

            public void Describe_data()
            {
                Console.WriteLine("Summary of Data\n===============");
                Console.WriteLine("Number of Features: {0}", number_of_features);
                Console.WriteLine("Number of items: {0}", number_of_items);
                Console.WriteLine("Target Feature: {0}", target);
                Console.Write("Target classes:");
                for(int j =0; j < target_classes.Length;j++) { Console.Write(target_classes[j] + "({0}),",j); }
                Console.WriteLine();
                /*for (int i = 0; i< number_of_features;i++)
                {
                    Console.Write(features[i] + ":");
                    if (feature_type[i] == typeof(double)) { Console.WriteLine("Continuous"); }
                    else
                    {
                        Console.Write("Discrete with " + feature_classes[i].Length + " classes\nClasses:");
                        for (int j = 0; j < feature_classes[i].Length; j++) { Console.Write(feature_classes[i][j] + "({0}),",j); }; Console.WriteLine();
                    }
                }
                for (int i = 0; i < 10; i++)
                {
                    Console.Write("{0}|", i);
                    for (int j=0;j< dim;j++)
                    {
                        Console.Write("{0},", input_array[i][j]);
                    }
                    Console.WriteLine("|{0}",output_array[i]);
                }*/
            }

        }

        /* We now write the methods that use the machine learning technique */
        

        public static void DecisionTreeTest(machine_learning_prob prob)
        {
            DecisionVariable[] attributes = new DecisionVariable[prob.dim];
            int offset = 0;
            for (int i =0;i< prob.number_of_features;i++)
            {
                if (prob.feature_type[i]== typeof(double))
                {
                    attributes[offset] = new DecisionVariable(prob.features[i], DecisionVariableKind.Continuous);
                    offset = offset + 1;
                }
                else
                {
                    for (int k = 0; k < prob.feature_classes[i].Length; k++)
                    {
                        attributes[offset] = new DecisionVariable(prob.features[i] + ":" + prob.feature_classes[i][k], DecisionVariableKind.Discrete);
                        offset = offset + 1;
                    }
                }
            }
            C45Learning teacher = new C45Learning(attributes);
            teacher.ParallelOptions.MaxDegreeOfParallelism = 1;
            var machine = teacher.Learn(prob.input_array, prob.output_array);
            Console.WriteLine("Machine trained");
            int[] predicted = machine.Decide(prob.input_array);
            double correct = 0;
            for (int i =0;i < prob.number_of_items; i++) { if (predicted[i]== prob.output_array[i]) { correct += 1; } }
            Console.WriteLine("Accuracy on training set {0}:", correct/System.Convert.ToDouble(prob.number_of_items));
        }


        public static void SupportVectorMachineTest(machine_learning_prob prob)
        {
            MulticlassSupportVectorLearning<Gaussian> svm = new MulticlassSupportVectorLearning<Gaussian>();
            svm.ParallelOptions.MaxDegreeOfParallelism = 1;
            var machine = svm.Learn(prob.input_array, prob.output_array);
            Console.WriteLine("Machine trained");
            
        }

        public static void KNearestNeighbor(machine_learning_prob prob)
        {
            /* This function takes the machine learning problem */
            KNearestNeighbors knn = new KNearestNeighbors();
            var machine = knn.Learn(prob.input_array, prob.output_array);
            Console.WriteLine("Machine trained");
            int[] p1 = new int[prob.number_of_items];
            int[] p2 = machine.Decide(prob.input_array,p1);
        }

        public static void LinearSVM(ref machine_learning_prob prob)
        {
            List<double[]>[] inputs_by_class = new List<double[]>[prob.target_classes.Length];
            for (int k=0; k < prob.target_classes.Length;k++)
            {
                inputs_by_class[k] = new List<double[]>();
            } 
            for (int i=0;i < prob.number_of_items; i++)
            {
                inputs_by_class[prob.output_array[i]].Add(prob.input_array[i]);
            }
            Accord.MachineLearning.VectorMachines.SupportVectorMachine[][] machines = new Accord.MachineLearning.VectorMachines.SupportVectorMachine[prob.target_classes.Length][];
            Console.WriteLine("machines training");
            int count =0;
            for (int i = 1; i < prob.target_classes.Length; i++)
            {
                
                machines[i] = new Accord.MachineLearning.VectorMachines.SupportVectorMachine[i];
                for (int j = 0; j < i; j++)
                {
                    int n = inputs_by_class[i].Count;
                    int m = inputs_by_class[j].Count;
                    int[] temp_out = new int[n + m];
                    for (int k = 0;k< m+n;k++) { temp_out[k] = (k < n) ? 1 : 0; }
                    LinearNewtonMethod svm = new LinearNewtonMethod();
                    machines[i][j] = svm.Learn(inputs_by_class[i].Concat(inputs_by_class[j]).ToArray(), temp_out);
                    count++;
                }
            }
            Console.WriteLine("{0} machines trained", count);
            double sum = 0;
            int[] predicted = new int[prob.number_of_items];
            for (int n = 0;n< prob.number_of_items;n++)
            {
                int[] scores = new int[prob.target_classes.Length];
                for (int k =0; k< prob.target_classes.Length;k++) { scores[k] = 0; }
                for (int i =1; i < prob.target_classes.Length;i++)
                {
                    for (int j=0;j < i;j++)
                    {
                        int s = machines[i][j].Decide(prob.input_array[n]) ? 1 : 0;
                        scores[i] += s;
                        scores[j] += 1 - s;
                    }
                }
                int max_index = 0;
                if (n < 10) { Console.Write("{0}:{1},", prob.target_classes[0], scores[0]); }
                for (int k=1;k<prob.target_classes.Length;k++)
                {
                    if (n < 10) { Console.Write("{0}:{1},", prob.target_classes[k], scores[k]); }
                    if (scores[k] > scores[max_index])
                    {
                        max_index = k;
                    }
                }
                predicted[n] = max_index;
                if (n < 10) { Console.WriteLine("\t Prediction is {0}", prob.target_classes[max_index]); }
                if (predicted[n] == prob.output_array[n]) { sum += 1.0; }
            }
            Console.WriteLine("Accuracy on training set is {0}%", sum / System.Convert.ToDouble(prob.number_of_items));
        }
    }
}
