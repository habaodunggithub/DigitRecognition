import process
import predict
from matplotlib import pyplot as plt

K = 10

def main():
    x_train, y_train = process.load_mnist("data/", kind="train")
    x_test, y_test = process.load_mnist("data/", kind="t10k")

    train_flat, train_chunk, train_histogram = process.extract_features(x_train)
    test_flat, test_chunk, test_histogram = process.extract_features(x_test)

    combined_train_flat = process.combine(train_flat, y_train)
    combined_train_chunk = process.combine(train_chunk, y_train)
    combined_train_histogram = process.combine(train_histogram, y_train)
    combined_test_flat = process.combine(test_flat, y_test)
    combined_test_chunk = process.combine(test_chunk, y_test)
    combined_test_histogram = process.combine(test_histogram, y_test)

    '''
    #Loop through K and test with t10k, plot accuracy

    flat_nearest_vectors = 'data/flat_nearest_vectors'
    chunk_nearest_vectors = 'data/chunk_nearest_vectors'
    histogram_nearest_vectors = 'data/histogram_nearest_vectors'

    predict.gen_nearest_k_vectors(combined_test_flat, combined_train_flat, flat_nearest_vectors, k = predict.K_MAX)
    predict.gen_nearest_k_vectors(combined_test_chunk, combined_train_chunk, chunk_nearest_vectors)
    predict.gen_nearest_k_vectors(combined_test_histogram, combined_train_histogram, histogram_nearest_vectors)

    flat_data = predict.load_binary(flat_nearest_vectors)
    chunk_data = predict.load_binary(chunk_nearest_vectors)
    histogram_data = predict.load_binary(histogram_nearest_vectors)
    data = [flat_data, chunk_data, histogram_data]

    test_range = range(1, 1001)
    predict.graph_accuracy_in_range(combined_test_flat, flat_data, test_range)
    '''
    
    extract_methods = {
        0: "FLAT",
        1: "CHUNK",
        2: "HISTOGRAM"
    }

    fig, ax = plt.subplots(nrows=3, ncols=3, sharex=True, sharey=True)
    ax = ax.flatten()

    cnt = 0
    for i in range(3):
        results = predict.predict_with_methods(x_test[i], K, extract_methods, combined_train_flat, combined_train_chunk, combined_train_histogram)

        for method_name, answer in results:
            ax[cnt].imshow(x_test[i], cmap="binary_r", interpolation="nearest")
            ax[cnt].set_title(f"{method_name}:{answer} - {'True' if (answer == y_test[i]) else 'False'}", fontsize=8)
            cnt += 1

    for a in ax:
        a.set_xticks([])
        a.set_yticks([])
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
