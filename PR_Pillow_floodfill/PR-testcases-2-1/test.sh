echo "---1000px---"
echo "master"
python3 ff_original.py rect-test-1000.jpg
echo "before"
python3 ff_partial_set.py rect-test-1000.jpg
echo "improved"
python3 ff_partial_set_imprvd.py rect-test-1000.jpg

echo "---2500px---"
echo "master"
python3 ff_original.py rect-test-2500.jpg
echo "before"
python3 ff_partial_set.py rect-test-2500.jpg
echo "improved"
python3 ff_partial_set_imprvd.py rect-test-2500.jpg

echo "---maze---"
echo "master"
python3 ff_original.py maze.bmp
echo "before"
python3 ff_partial_set.py maze.bmp
echo "improved"
python3 ff_partial_set_imprvd.py maze.bmp
