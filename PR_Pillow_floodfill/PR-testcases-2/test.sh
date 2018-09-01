echo "master"
python3 ff_original.py rect-test-1000.jpg
echo "1"
python3 ff_partial_set.py rect-test-1000.jpg
echo "2"
python3 ff_partial_set_imprvd.py rect-test-1000.jpg

echo "master"
python3 ff_original.py rect-test-2500.jpg
echo "1"
python3 ff_partial_set.py rect-test-2500.jpg
echo "2"
python3 ff_partial_set_imprvd.py rect-test-2500.jpg

echo "master"
python3 ff_original.py bf.jpg
echo "1"
python3 ff_partial_set.py bf.jpg
echo "2"
python3 ff_partial_set_imprvd.py bf.jpg

echo "master"
python3 ff_original.py maze.bmp
echo "1"
python3 ff_partial_set.py maze.bmp
echo "2"
python3 ff_partial_set_imprvd.py maze.bmp
